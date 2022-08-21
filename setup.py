from setuptools import setup, find_packages
setup(
    name = 'Prestige-CLI',
    version = '0.0.1',
    packages = find_packages(),
    install_requires = [
        'click',
        'solana',
        'borsh_construct',
        'base58',
        'gidgethub',
        'aiohttp',
        'asyncio'
        ],
    entry_points = '''
    [console_scripts]
    prestige=prestige_cli:entry
    '''
)