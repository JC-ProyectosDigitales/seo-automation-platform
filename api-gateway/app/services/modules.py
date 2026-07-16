import os

from dotenv import load_dotenv


load_dotenv()


def get_modules():

    modules = {}

    for key, value in os.environ.items():

        if key.startswith("SEO_"):

            module_name = (
                key.replace("SEO_", "")
                .lower()
                .replace("_", "-")
            )

            modules[module_name] = value

    return modules