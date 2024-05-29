
p_c:
	git add --all && git commit -m "push code" && git push


u_d:
	python add_tag_openapi.py
	python image_to_avif.py

	docker-compose down
	docker-compose up -d



t:
	docker build -t mock_server .