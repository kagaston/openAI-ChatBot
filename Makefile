.PHONY: install update init stage commit push pull new-branch switch-branch merge-branch status

install:
	pip install --upgrade pip
	pip install pip-tools
	pip install -r requirements.txt

update:
	pip-compile --generate-hashes --resolver=backtracking --output-file=requirements.txt requirements.in
	pip-sync requirements.txt

init:
	git init

stage:
	git add .

commit:
	git commit -m "Commit message"

push:
	git push origin <branch-name>

pull:
	git pull origin <branch-name>

new-branch:
	git checkout -b <branch-name>

switch-branch:
	git checkout <branch-name>

merge-branch:
	git merge <branch-name>

status:
	git status