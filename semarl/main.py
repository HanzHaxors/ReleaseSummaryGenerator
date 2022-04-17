from os import getcwd
from pathlib import Path
from git import Repo

import sys
import git

argv = sys.argv[1:]
if len(argv) != 2:
	print("USAGE:")
	print("py main.py <start> <end>")
	print("\n`start` and `end` could be the commit hash or tag")
	exit()

commitTypes = {
	"feat": "New Features",
	"fix": "Bug Fixes",
	"docs": "Documentation",
	"style": "Misc",
	"refactor": "Misc",
	"test": "Misc",
	"chore": "Misc"
}

entries = {
	"New Features": [],
	"Bug Fixes": [],
	"Documentation": [],
	"Misc": []
}

class Entry(object):
	def __init__(self, type, scope, summary):
		self.type = type
		self.scope = scope
		self.summary = summary

	def __str__(self):
		scope = self.scope
		if scope != '':
			scope = "to " + scope

		return f" - {self.summary.strip().capitalize()} {scope}."

def run():
	repo = None
	cwd = Path(getcwd())
	#cwd = Path('/mnt/e/GitHub Repository/fabuya')
	start = argv[0]
	end = argv[1]

	while repo is None:
		try:
			repo = Repo(cwd)
		except git.exc.InvalidGitRepositoryError:
			# CWD is not git repository,
			# check parent directory
			cwd = cwd.parent

	assert not repo.bare

	start = repo.commit(start)
	end = repo.commit(end)
	commits = [end]

	while True:
		end = end.parents[0]
		commits.append(end)
		if end.binsha != start.binsha:
			break

	for commit in commits:
		msg = commit.message.strip()
		msgs = msg.split('\n')
		for msg in msgs:
			indicator = msg.split(':')[0]
			type = ""

			for ctype in commitTypes.keys():
				if indicator.lower().startswith(ctype):
					type = ctype
					break

			scope = indicator.replace(type, '').replace('(', '').replace(')', '')
			summary = msg.split(':', maxsplit=1)[1]

			newEntry = Entry(type, scope, summary)
			entries[commitTypes[newEntry.type]].append(newEntry)

	for key in entries.keys():
		print(key)
		for entry in entries[key]:
			print(str(entry))
		print()