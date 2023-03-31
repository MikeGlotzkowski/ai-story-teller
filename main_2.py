from flask import Flask, request
from flask import render_template_string
import replicate
import openai
import os
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

def create_story(story_to_tell: str):
    app.logger.info(f'Asking gpt for the story....')

    full_story_unparsed = ask_gpt(story_to_tell)
    app.logger.info(f"The full story from gpt is: {full_story_unparsed}")
    shards = full_story_unparsed.split("Section")[1:]
    clean_shards = [shard[4:] for shard in shards]

    app.logger.info(f'Got shards for story.')
    return clean_shards


def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def get_summary_from_gpt(story_section):
    promt = f'Please summarize this text to 10 words I can sent to an stable-diffusion AI model to generate a fitting image: {story_section}'
    app.logger.info(f"Asking gpt to summarize:\n{promt}")
    summary = ask_gpt(promt)
    app.logger.info(f"GPT said: {summary}")
    return summary


def get_link_to_picture_for_prompt(prompt: str):
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={"prompt": prompt}
    )
    return output[0]


@app.route('/')
def index():
    return '''
        <form action="/story" method="POST">
            <label for="story">Enter some text:</label><br>
            <input type="text" id="story" name="story"><br>
            <input type="submit" value="Submit">
        </form>
    '''


@app.route('/story', methods=['POST'])
def get_story():

    openai.api_key = os.getenv("OPENAI_API_KEY")

    story_to_tell = request.form['story']
    app.logger.info(
        f'Story entred in FE: {story_to_tell}')
    story_to_tell_with_wrapper = f'for the following promt, create a small story. It should be split in 4 "sections". each section should 4 sentences long and begin with "Section n:". please only return the story and seperate the sections with "---". The promt is: {story_to_tell}'
    app.logger.info(
        f'Promt we are sending to gpt to create the story: {story_to_tell_with_wrapper}')
    story: list = create_story(story_to_tell_with_wrapper)
    app.logger.info("Now we summarize the story.")
    short_story: list = [get_summary_from_gpt(section) for section in story]
    app.logger.info('Short story created.')
    stories_html = ''

    for i, section in enumerate(story):
        short_section = short_story[i]
        app.logger.info(f"getting picture for short_section: {short_section}")
        link_to_picture = get_link_to_picture_for_prompt(short_section)
        app.logger.info(f"Link: {link_to_picture}")
        stories_html += f'''
            <div>
                <h2>{short_section}</h2>
                <p>{section}</p>
                <img src='{link_to_picture}'/>
            </div>
        '''
    app.logger.info("Created html for all sections!")

    html = f'''
        <html>
            <head>
                <title>Story</title>
            </head>
            <body>
                {stories_html}
            </body>
        </html>
    '''

    return render_template_string(html)


if __name__ == '__main__':
    app.run()
