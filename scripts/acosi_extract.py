import json
from pipeline import run_pipeline
from pickle import dump
from utils import get_file_path, format_output, get_args, dump_output

category_file_path = get_file_path("shoes-acosi-cate-list.json")

with open(category_file_path, "r") as f:
    shoes_cate_list = json.load(f)


def get_ACOSI_extract_prompt():
    prompt = """
    Given a product review, 
    extract the corresponding ACOSI (Aspect-Category-Opinion-Sentiment-Implicit/Explicit) quintuples.\n

    Each quintuple is comprised of 5 components:\n
    - Aspect: The span of text in the review that indicates the particular aspect that the customer is referring to. 
              Aspects are not always explicitly stated; if this is the case, use a NULL label for the aspect.\n
    - Category: The category of the aspect, selected from the following list: {category_list}\n
    - Sentiment: The polarity of the sentiment: positive, negative, or neutral.\n
    - Opinion: The span of text in the review that indicates the opinion that expresses the sentiment.
               Opinions are not always explicitly stated; if this is the case, please try to identify the span of text that best expresses the sentiment implicitly.\n
    - Implicit Indicator: Indicates whether the opinion is implicit or explicit (indirect or direct).
    \n\n
    """

    category_list = "[" + ",".join(shoes_cate_list) + "]"

    prompt = prompt.format(category_list=category_list)

    response_head = "ACOSI quintuples:"

    example1 = f"""
    Example 1:\n\n

    Review: the design is great poor color choices too bland . color choices from previous shoes was much better . \n

    Response: \n
    {response_head} [(Aspect: NULL, Category: appearance#form, Sentiment: positive, Opinion: "design is great", Implicit/Explicit: direct), 
                       (Aspect: NULL, Category: appearance#color, Sentiment: negative, Opinion: "poor color choices", Implicit/Explicit: direct), 
                       (Aspect: "shoes", Category: appearance#color, Sentiment: negative, Opinion: "color choices from previous shoes was much better", Implicit/Explicit: indirect)]
                       \n\n

    """

    example2 = f"""
    Example 2: \n\n

    Review: had to order a larger size than what i normally wear . shoe would be better if offered as an adjustable shoe . shoe is overpriced for quality . i bought cheaper slides in the past that were more comfortable . \n

    Response: \n
    {response_head} [(Aspect: NULL, Category: performance#sizing_fit, Sentiment: neutral, Opinion: "had to order a larger size than what i normally wear", Implicit/Explicit: direct), 
                       (Aspect: NULL, Category: contextofuse#purchase\\\\_context, Sentiment: negative, Opinion: "had to order a larger size than what i normally wear", Implicit/Explicit: direct), 
                       (Aspect: "shoe", Category: appearance#form, Sentiment: neutral, Opinion: "would be better if offered as an adjustable shoe", Implicit/Explicit: direct), 
                       (Aspect: "shoe", Category: cost/value, Sentiment: negative, Opinion: "overpriced for quality", Implicit/Explicit: direct), 
                       (Aspect: "slides", Category: cost/value, Sentiment: negative, Opinion: "i bought cheaper slides in the past that were more comfortable", Implicit/Explicit: direct), 
                       (Aspect: "slides", Category: performance#comfort, Sentiment: negative, Opinion: "i bought cheaper slides in the past that were more comfortable", Implicit/Explicit: direct)]
                       \n\n
    """

    examples = [example1, example2]

    return prompt, examples, response_head


def main(args):
    prompt, examples, response_head = get_ACOSI_extract_prompt()
    output, response_key = run_pipeline(
        args, prompt, examples, absa_task="acosi-extract"
    )
    formatted_output = format_output(output, response_key, response_head)
    dump_output(args.output_file, formatted_output)


if __name__ == "__main__":
    args = get_args()
    main(args)
