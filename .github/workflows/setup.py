from setuptools import setup, find_packages

setup(
    name='email-validator',  # Replace with your package name
    version='0.0.0',  # Start with version 0.1.0
    description='Separate valid email domains from diposable domains easily',
    packages=find_packages(),
    include_package_data=True,  # Include data files if needed
    install_requires=[  # List dependencies required for your package
        'disposable_email-domains',
        'openpyxl',
        'pandas',
        'scikit-learn',
        'streamlit',
        'xgboost',
    ],
    entry_points={  # Optional: Define entry points for scripts (if applicable)
        'console_scripts': [
            'main.py = your_package_name.script:main_function',
        ],
    },
)
