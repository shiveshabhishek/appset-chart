import yaml
from flask import Flask, render_template, request, send_file
from io import BytesIO
import git
from gitcommit import commit_file
import os
import logging

logging.basicConfig(level=logging.INFO)

username = os.environ.get('USERNAME')
token = os.environ.get('TOKEN')


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        deployment_method = request.form.get('deployment_method')
        plainYAML = deployment_method == 'plainYAML'
        helm = deployment_method == 'helm'
        
        name = request.form['name']
        project = request.form['project']
        repoURL = request.form['repoURL']
        namespace = request.form['namespace']
        url = request.form['url']
        path = request.form['path']
        targetRevision = request.form['targetRevision']

        stages = request.form.getlist('stages[]')
        
        env_names = request.form.getlist('env_name[]')
        env_stages = request.form.getlist('env_stage[]')
        env_namespaces = request.form.getlist('env_namespace[]')
        env_urls = request.form.getlist('env_url[]')
        env_paths = request.form.getlist('env_path[]')
        env_revisions = request.form.getlist('env_target_revision[]')
        env_projects = request.form.getlist('env_project[]')
        if deployment_method == 'helm':
            env_valuefiles = request.form.getlist('env_valuefiles[]')

        environments = []
        if deployment_method == 'helm':
            for i in range(len(env_names)):
                environments.append({
                    'name': env_names[i],
                    'url': env_urls[i],
                    'path': env_paths[i],
                    'targetRevision': env_revisions[i],
                    'namespace': env_namespaces[i],
                    'stage': env_stages[i],
                    'valueFiles': env_valuefiles[i],
                    'project': env_projects[i]
                })
        else:
            for i in range(len(env_names)):
                environments.append({
                    'name': env_names[i],
                    'url': env_urls[i],
                    'path': env_paths[i],
                    'targetRevision': env_revisions[i],
                    'namespace': env_namespaces[i],
                    'stage': env_stages[i],
                    'project': env_projects[i]
                })

        data = {
            'plainYAML': plainYAML,
            'helm': helm,
            'name': name,
            'project': project,
            'repoURL': repoURL,
            'namespace': namespace,
            'url': url,
            'path': path,
            'targetRevision': targetRevision,
            'stages': {
                'key': 'stage',
                'values': stages
            },
            'environments': environments
        }

        yaml_data = yaml.dump(data, default_flow_style=False)

        output = BytesIO()
        output.write(yaml_data.encode('utf-8'))
        output.seek(0)
        download_name = f"{name}-values.yaml"
        response = send_file(output, mimetype='application/x-yaml', as_attachment=True, download_name=download_name)

        commit_file(download_name, yaml_data)
        return response
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
