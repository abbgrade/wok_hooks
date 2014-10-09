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

    <div>
        {% for comment in page.subpages %}
            <div>
            {{comment.author}}
            {{ comment.datetime.strftime('%c') }}
            {{ comment.content }}
            </div>
        {% endfor %}

        <div>
            <a class="btn btn-primary" href="mailto:YOUR_CONTACT_EMAIL@EXAMPLE.TLD?subject={{ page.category[0]|safe }}%2F{{ page.slug|safe }}">
                Add Comment
            </a>
        </div>
    </div>
    
Don't forget to replace *comment@example.tld* in the comment link.

## Janitor

### clean_temp_files

Remove temp files before generating the website.

## Timeline

Generation of (small) (activity based) posts.

### Example Template

    {% for events in site.slugs['timeline'].subpages|sort(attribute='datetime',reverse=True)|batch(10) %}
        {% if loop.first %}
            {% for event in events %}
                <div timeline_update">
                    <div class="timeline_actions_json" style="display:none">
                        {{ event.actions }}
                    </div>
                    <div>
                        {{ event.datetime.strftime('%x') }}
                    </div>
                    <p>
                        {{ event.content }}
                    </p>
                </div>
            {% endfor %}
        {% endif %}
    {% endfor %}

### add_diaspora_posts_to_timeline

Add public diaspora posts to the timeline.

#### Sample config *diaspora.conf*:

	{
		"pod": "joindiaspora.com", 
		"user": "username"
	}

### add_github_posts_to_timeline

Add public github activities to the timeline.

#### Sample config *github.com*:
	
	{
		"user": "abbgrade"
	}

### add_diggs_to_timeline

Add public digg recommendations to the timeline.

Get your id from the digg-setting page on "Privacy/Diggs" and set it to *Public*.
An url appears, which contains the id between *http://digg.com/user/* and */diggs.rss*.
Add that string in the *digg.config*

	{
		"secret_user_id": "#HERE#"
	}

### add_wikipedia_actions_to_timeline

 Add wikipedia contributions to the timeline.

#### Sample config *wikipedia.conf*:

    {
        "lang": "de",
        "user": "username"
    }

## VCard

Import of contact data from vcard files.

### add_vcard_to_contact

Read vcard files adds the contact data as metadata in generated markdown files.

### Example Template
    
    {% set person = page %}
    
    <dl typeof="schema:Person">
        <span property="schema:name" content="{{ person.name }}"></span>
        <span property="schema:url" content="{{ person.url }}"></span>
    
        {% if person.email %}
    
            <dt>
                EMail
            </dt>
            <dd>
                <a href="mailto:{{ person.email }}" property="schema:email">
                    {{ person.email }}
                </a>
    
            </dd>
    
        {% endif %}
    
        {% if person.gpg %}
    
            <dt>
                PGP
            </dt>
            <dd>
                <a href="{{ person.gpg[1] }}">
                   Public Key
                </a>
                - Fingerprint:
                <small>
                    {{ person.gpg[0] }}
                </small>
            </dd>
    
        {% endif %}
    
        {% if person.links %}
            {% for link_title, link_uri in person.links %}
    
            <dt>
                {{ link_title }}
            </dt>
            <dd>
                <a href="{{ link_uri }}" rel="me" property="schema:sameAs">
                    {{ link_uri }}
                </a>
            </dd>
    
            {% endfor %}
        {% endif %}
    
    </dl>
