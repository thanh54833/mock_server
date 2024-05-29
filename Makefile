
p_c:
	git add --all && git commit -m "push code" && git push


u_d:
	# docker-compose down --volumes --rmi all
	python3 -m pip install -r requirements.txt

	python3 add_tag_openapi.py
	python3 image_to_avif.py

	git add --all && git commit -m "push code" && git push origin HEAD:main


#	docker-compose down
#	docker-compose up -d


image_to_avif:
	python3 -m pip install pillow

t:
	docker build -t mock_server .