import setuptools

setuptools.setup(
    name="streamlit-datagrid",
    version="0.0.1",
    author="victorC97",
    author_email="victor.cour@telecomnancy.net",
    description="Scrollable data grid for listing items.",
    long_description="Streamlit component based on Typescript/MUI/React to display large list of items.",
    long_description_content_type="text/plain",
    url="https://github.com/victorC97/streamlit_datagrid",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
    setup_requires=['wheel']
)
