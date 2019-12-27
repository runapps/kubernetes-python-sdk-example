podTemplate(
	label: 'mypod',
	volumes: [
		emptyDirVolume(mountPath: '/etc/gitrepo', memory: false),
		hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock')
	],
	containers:
	[
	    containerTemplate(name: 'git', image: 'alpine/git', ttyEnabled: true, command: 'cat'),
	    containerTemplate(name: 'python', image: 'python:3.7.2', command: 'cat', ttyEnabled: true),
	    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true,
	    	envVars: [secretEnvVar(key: 'DOCKER_HUB_PASSWORD', secretName: 'docker-hub-password', secretKey: 'DOCKER_HUB_PASSWORD')]
	    )
    ]
)
{
    node('mypod') {
        stage('Clone repository') {
            container('git') {
                sh 'git clone -b master https://github.com/alicek106/kubernetes-python-sdk-example.git /etc/gitrepo'
            }
        }
        stage('Test source codes') {
            container('python') {
                sh 'pip install -r /etc/gitrepo/requirements.txt'
                sh 'python /etc/gitrepo/__main__.py /etc/gitrepo/unit_test'
                junit 'unit_test/jenkins_output/*.xml'
            }
        }
        stage('Build and push docker image'){
            container('docker') {
                sh 'docker login -ualicek106 -p$DOCKER_HUB_PASSWORD'
                sh 'docker build /etc/gitrepo/ -t alicek106/kubernetes-python-sdk-example --no-cache'
                sh 'docker push alicek106/kubernetes-python-sdk-example'
            }
        }
    }
}