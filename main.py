import replicate
import openai
import os


def get_link_to_pricture_for_promt(promt: str):
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={"prompt": promt}
    )
    return output


openai.api_key = os.getenv("OPENAI_API_KEY")

def promt_user():
    user_input = input("Enter some text: ")
    return user_input


def create_story(story_to_tell: str):
    full_story_unparsed = ask_gpt(story_to_tell)

    shards = full_story_unparsed.split("Section")[1:]
    clean_shards = [shard[4:] for shard in shards]

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
    return ask_gpt(promt)


def print_a_story_section(long_section, short_section, link):
    print(f"Headline: {short_section}")
    print("_____________")
    print(long_section)
    print(f"Link: {link}")
    print("\n\n")


def main():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    # link = run_model_with_promt(promt_user())
    # print(f"Follow this link: {link}")
    story_to_tell = promt_user()
    story_to_tell_with_wrapper = f'for the following promt, create a small story. It should be split in 4 "sections". each section should 4 sentences long. please only return the story and seperate the sections with "---". The promt is: {story_to_tell}'
    story: list = create_story(story_to_tell_with_wrapper)

    short_story: list = [get_summary_from_gpt(section) for section in story]

    print()

    for i, section in enumerate(story):
        short_section = short_story[i]
        print_a_story_section(section, short_section, get_link_to_pricture_for_promt(short_section))


if __name__ == '__main__':
    main()
