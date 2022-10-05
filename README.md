# arXiv_metadata
get metadata for all arXiv's articles, updated daily with new articles(via OAI-PMH)

arXiv에서 제공하는 OAI protocol을 이용하여 매일 업데이트되는 arXiv의 article metadata(full-text pdf url을 포함)들을 json 파일로 저장합니다.

## Use

```
git clone https://github.com/jiyoung98/arXiv_metadata.git
cd arXiv_metadata
python3 -m venv venv
source ./venv/bin/activate
(venv) pip install -r requirements.txt
(venv) python main.py --start 2021-01-15 --end 2021-01-22 --set cs #예시
```

```
# OUT        
CURSOR_NOW: 0/1431
CURSOR_NOW: 1000/1431
```

## Details
* 예시는 timestamp : 2021-01-15 ~ 2021-01-22, set : cs 의 결과를 반환합니다.
* 가능한 set의 목록은 http://export.arxiv.org/oai2?verb=ListSets 를 참조하십시오.(cs, econ 등 올바른 setSpec을 입력하지 않으면 빈 json이 반환됩니다.)
* start, end, set 인자를 모두 주지 않을 시 현 시점 arXiv에서 제공하는 모든 article의 metadata가 반환됩니다.
  ```
  (venv) python main.py  
  CURSOR_NOW: 0/2137197
  CURSOR_NOW: 1000/2137197
  CURSOR_NOW: 2000/2137197
  CURSOR_NOW: 3000/2137197 # 2021.10.05 기준
  ```



