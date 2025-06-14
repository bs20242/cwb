from setuptools import setup, find_packages

try:
    with open('requirements.txt') as f:
        required = f.read().splitlines()
except FileNotFoundError:
    required = []

setup(
    name="codewise_lib",
    version="0.2.0", # Aumentamos a versão para refletir as novas funcionalidades
    author="BPC",
    description="Uma ferramenta para análise de código e automação de PRs com CrewAI.",
    package_dir={
        'codewise_lib': 'docs/code_wise/codewise/src/codewise',
        'scripts': 'scripts'
    },
    packages=['codewise_lib', 'scripts'],
    include_package_data=True,
    install_requires=required,
    python_requires='>=3.11',

    # Adicionamos o novo comando 'codewise-init'
    entry_points={
        'console_scripts': [
            'codewise-pr=scripts.codewise_review_win:main',
            'codewise-init=scripts.install_hook:main',
        ],
    },
)