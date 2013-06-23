wok_hooks
=========

Some utile hooks for wok, the static website generator.

## Distribution

### hook_distribute

Upload the website output via ftp or ssh/sftp.

Sample config *distribute.conf* for SSH:

	{
		"sftp_password": "secret", 
		"sftp_host": "example.tld", 
		"sftp_user": "username", 
		"output_path": "/usr/share/nginx/www/", 
		"type": "sftp", 
		"sftp_port": "22"
	}

## hook_janitor

Remove temp files before generating the website.

## Timeline

Generation of (small) (activity based) posts.

### hook_diaspora

Add public diaspora posts to timeline.

Sample config *diaspora.conf*:

	{
		"pod": "joindiaspora.com", 
		"user": "username"
	}

### hook_github

Add public github activities to timeline.

Sample config *github.com*:
	
	{
		"user": "abbgrade"
	}