작성중,,(issue로 등록해야함)

해야할 게 많음
1. service부분을 class로 만들어야 함 그래야지 확장성을 가질 수 있으니까..  
    근데 충격적이게도 공식 문서에는 무조건적인 def로 작성되어 있음.ㅠㅠ 그리고 class로 작성되어있는 부분이 존재하는데 1.0.19 version부터는 그 클래스로 작성된 부분의 module이 사라져있음
- 사라진 module : 더 있을 수 있는데 여튼 이 부분은 없어져있음.
    - bentoml.BentoService
    - bentoml.api
2. rfai의 inference부분을 bentoml로 만들 수 있을 것 같음.
    bentoml.Runnable을 부모클래스로 참조해서 어떻게 하면 될 것 같은데 이게 더 빠를지 모름.
3. 응답속도에 대한 테스트가 필요함..
4. Docker 환경으로 설치할 수 있도록 준비.
