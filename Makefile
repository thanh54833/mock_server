
p_c:
	git add --all && git commit -m "push code" && git push


u_d:
	python3 mockoon_to_openapi.py
	python3 image_to_avif.py

	# git add --all && git commit -m "push code" && git push origin HEAD:main
	docker-compose down
	docker-compose up -d



convert_avif:
	python download_image.py

t:
	docker build -t mock_server .