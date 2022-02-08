#  Create Anki cards by DeepL

Tested only on Mac so if you will have some problems feel free to open issues.

## Motivation
When I watch series I store subtitles that I can't translate to a txt file and then create from these sentences Anki cards.
So, this script helps me with this job.

## Requirements

Anki app [link](https://apps.ankiweb.net/)

Anki-Connect (instruction how to setup Anki-Connect [link](https://foosoft.net/projects/anki-connect/))

python3

pip3

DeepL Api-Key (you can get it by this [link](https://www.deepl.com/pro-api?cta=header-pro-api))

## Example of usage
```  
git clone https://github.com/lysenko-sergey-developer/create-anki-cards-by-deepl.git
cd create-anki-cards-by-deepl
pip3 install -r requirements.txt 
python3 create-anki-cards-by-deepl.py --input example-input.txt --target-lang RU --name "my deck" --auth-key=<AUTH-KEY>
```

Try print help if you want know all options
```
python3 create-anki-cards-by-deepl.py --help
```

## TODO
- [ ] Add user readable output when app process some issues

