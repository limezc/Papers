import os

from openai import OpenAI

AIGC_TASK_TYPES = [
    "图像生成",
    "图像编辑",
    "视频生成",
    "视频编辑",
    "3D生成",
    "3D编辑",
    "多模态大语言模型",
    "其他多任务",
]
AIGC_TASK_TYPES_ENGLISH = [
    "image generation",
    "image editing",
    "video generation",
    "video editing",
    "3D generation",
    "3D editing",
    "multimodal large language model",
    "other multi-task",
]

# the prompt of the gpt for the type of the paper
PROMPT = 'Determine whether the paper belongs to the AIGC direction based on the abstract of the paper. If it does not, return a -1. If it does, start from ["image generation", "image editing", "video generation", "video editing", "3D generation", "3D editing", "multimodal large language model", "other multi-task"] find the corresponding category among these categories and return the id of the corresponding category. Note that the result only needs to return a number. The abstract of the paper is as follows: '


def post_processing(res):
    nums = [i for i in range(-1, len(AIGC_TASK_TYPES))]
    for num in nums:
        if str(num) in res:
            return num
    return -1


def gpt_analyze_abstract(abstract):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url="https://api.pumpkinaigc.online/v1",
    )
    # gpt-3.5-turbo, gpt-4, and gpt-4-turbo-preview
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": PROMPT + abstract}],
        stream=False,
    )
    return post_processing(response.choices[0].message.content.strip())


def moonshot_analyze_abstract(abstract):
    client = OpenAI(
        api_key=os.environ.get("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )

    # moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[{"role": "user", "content": PROMPT + abstract}],
        temperature=0.3,
    )

    return post_processing(response.choices[0].message.content.strip())


analysis_engine = {"gpt": gpt_analyze_abstract, "moonshot": moonshot_analyze_abstract}


if __name__ == "__main__":
    abstract = "Recent large-scale text-driven synthesis models have attracted much attention thanks to their remarkable capabilities of generating highly diverse images that follow given text prompts. Such text-based synthesis methods are particularly appealing to humans who are used to verbally describe their intent. Therefore, it is only natural to extend the text-driven image synthesis to text-driven image editing. Editing is challenging for these generative models, since an innate property of an editing technique is to preserve most of the original image, while in the text-based models, even a small modification of the text prompt often leads to a completely different outcome. State-of-the-art methods mitigate this by requiring the users to provide a spatial mask to localize the edit, hence, ignoring the original structure and content within the masked region. In this paper, we pursue an intuitive prompt-toprompt editing framework, where the edits are controlled by text only. To this end, we analyze a text-conditioned model in depth and observe that the cross-attention layers are the key to controlling the relation between the spatial layout of the image to each word in the prompt. With this observation, we present several applications which monitor the image synthesis by editing the textual prompt only. This includes localized editing by replacing a word, global editing by adding a specification, and even delicately controlling the extent to which a word is reflected in the image. We present our results over diverse images and prompts, demonstrating high-quality synthesis and fidelity to the edited prompts."
    res_gpt = gpt_analyze_abstract(abstract)
    res_kimi = moonshot_analyze_abstract(abstract)
    print("gpt prediction: {}".format(AIGC_TASK_TYPES[res_gpt]))
    print("moonshot prediction: {}".format(AIGC_TASK_TYPES[res_kimi]))
