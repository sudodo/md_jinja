from setuptools import setup, find_packages

setup(
    name="md_jinja",
    version="0.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "md_jinja = md_jinja.render_md:main"
        ]
    },
)