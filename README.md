# wok_hooks

Some utile hooks for [wok](https://github.com/mythmon/wok), the static website generator.

Features are a comment system, auto upload and a timeline based on external sources like github or diaspora.

## Distribution

### distribute_output

Upload the website output via ftp or ssh/sftp.

#### Sample config *distribute.conf* for SSH:

	{
		"sftp_password": "secret", 
		"sftp_host": "example.tld", 
		"sftp_user": "username", 
		"output_path": "/usr/share/nginx/www/", 
		"type": "sftp", 
		"sftp_port": "22"
	}

## Comments

The comment system is based on wok subpages, so it will work for blogposts but not for the blog itself.

### add_mails_to_comments

Loads comments from IMAP.
The referenced page is defined by the page slug as mail subject.
So an simple mailto-link and an for-loop for the comments in the page HTML will be neccessary to have comments in the page.

#### Example Config

    {
        "password": "secret password magic", 
        "user": "username", 
        "server": "mailserver.example.tld"
    }

#### Example Template

    {% block comments %}
    <hr />
    <div>
        <h2>Comments</h2>
    {% for comment in page.subpages %}
    	<div>
    		{{ comment.datetime.strftime('%c') }} - {{comment.author}}
    		<blockquote>
    			{{ comment.content }}
    		</blockquote>
    	</div>
    {% endfor %}
    	<a href="mailto:comment@example.tld?subject={{ page.category[0]|safe }}%2F{{ page.slug|safe }}">Add Comment</a>
    	Please do not edit the subject! The email address will not published!
    </div>
    {% endblock %}
    
Don't forget to replace *comment@example.tld* in the comment link.

## Janitor

### clean_temp_files

Remove temp files before generating the website.

## Timeline

Generation of (small) (activity based) posts.

### add_diaspora_posts_to_microblog

Add public diaspora posts to timeline.

#### Sample config *diaspora.conf*:

	{
		"pod": "joindiaspora.com", 
		"user": "username"
	}

### add_github_posts_to_microblog

Add public github activities to timeline.

#### Sample config *github.com*:
	
	{
		"user": "abbgrade"
	}
