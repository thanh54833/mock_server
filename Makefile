
p_c:
	git add --all && git commit -m "push code" && git push


u_d:
	python3 mockoon_to_openapi.py
	python3 image_to_webp.py

	# git add --all && git commit -m "push code" && git push origin HEAD:main
	docker-compose down
	docker-compose up -d


# brew install webp
convert_webp:
	python3 image_to_webp.py

t:
	docker build -t mock_server ffff.



# docker-compose down --volumes --rmi all