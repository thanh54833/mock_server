
p_c:
	git add --all && git commit -m "push code" && git push


u_d:
	python add_tag_openapi.py
	docker-compose down
	docker-compose up -d