import os
import re
import sys
from time import sleep

AGREEMENT_STR = '''Are you sure, you want to change the remote url:
{old_url} \nto a new one: \n{new_url} \n[y/n]: '''

REG_EX = {
	'CURRENT_USERNAME': r'https://github.com/(\w+)',
	'CHANGE_USERNAME': r'https://github.com/{}',
	'REMOTE_URL': r'	url = (\w+.*)',
}

INPUT = {
	'AGREEMENT': '''Are you sure, you want to change the remote url:
{old_url} to a new one: {new_url} \n[y/n]: ''',
	'OLD_USERNAME': 'Type your old username: ',
	'NEW_USERNAME': 'Type your new username: ',
	'ALL_PATH': 'Type here /path/to/your/projects_directory : ',
	'ONE_PATH': 'Type here /path/to/your/root/project_directory \n(where did you inited git): '
}

OUTPUT = {
	'SUB_SUCCESS': 'Remote url is changed\n',
	'SUCCESS': 'All the projects inited with git are changed',
	'ISSUE': {
		'WRONG_DIR': 'Provided directory does not exist',
		'ERROR': '''Error in {proj_dir} :\nUsername inited in a git configuration file
does not match the name you want to change. Either you provided a wrong old_username or
you did not remote the project.
			''',
		'NOTGIT': '''Issue in {pr_dir}:
.git does not exist
								''',
		'NOTREMOTE': 'Something went wrong, possibly this git does not have a remote'
	}
}


def find_project_dirs(projects_dir):
	if os.path.isdir( projects_dir ):
		os.system( 'ls -d -1 {pr_dir}/*/ > projects.txt'.format( pr_dir=projects_dir ) )
		projects_f = open( 'projects.txt', 'r' )
		projects = projects_f.read()
		projects_f.close()
		projects_list = projects.split( '\n' )
		return projects_list
	else:
		print( OUTPUT['ISSUE']['WRONG_DIR'] )


def has_git(project_dir):
	return (os.path.isdir( project_dir + '.git' ))


def change_remote(path_to_proj, old_username, new_username):
	if has_git(path_to_proj):
		path_to_config = path_to_proj + '.git/config'
		config_file = open( path_to_config, "r" )
		config_str = config_file.read()
		config_file.close()
		current_username_list = re.findall( REG_EX['CURRENT_USERNAME'], config_str )
		if len( current_username_list ) > 0:
			current_username = current_username_list[0]
			if current_username == old_username:
				config_file = open( path_to_config, 'w' )
				result_config_str = re.sub( REG_EX['CHANGE_USERNAME'].format( old_username ),
				                            REG_EX['CHANGE_USERNAME'].format( new_username ),
				                            config_str )
				old_url = re.findall( REG_EX['REMOTE_URL'], config_str )[0]
				new_url = re.findall( REG_EX['REMOTE_URL'], result_config_str )[0]
				agreement_text = INPUT['AGREEMENT'].format(
					old_url=old_url,
					new_url=new_url
				)
				agreement = True if input( agreement_text ) == 'y' else False
				if agreement:
					config_file.write( result_config_str )
					print( OUTPUT['SUB_SUCCESS'] )

				config_file.close()
			else:
				error = OUTPUT['ISSUE']['ERROR'].format( proj_dir=path_to_proj )
				print( error )
		else:
			print( OUTPUT['ISSUE']['NOTREMOTE'] )
		return
	else:
		issue = OUTPUT['ISSUE']['NOTGIT'].format( pr_dir=path_to_proj )
		print( issue )


def main():
	old_username = input( INPUT['OLD_USERNAME'] )
	new_username = input( INPUT['NEW_USERNAME'] )

	if sys.argv[1] == 'all':
		projects_directory = input( INPUT['ALL_PATH'] )
		projects_dirs = find_project_dirs( projects_directory )
		for project in projects_dirs:
			if project != '':
				change_remote( project, old_username, new_username )
			sleep( 0.01 )
		print(OUTPUT['SUCCESS'])
	elif sys.argv[1] == 'one':
		path_to_project = input( INPUT['ONE_PATH'] ) + '/'
		change_remote( path_to_project, old_username, new_username )
	os.remove( "projects.txt")



if __name__ == '__main__':
	main()
