# deploy
GIT=git
CTL=supervisorctl -s unix:///tmp/supervisor.sock
worker_list=swan:swan-schedule
start:
	for worker in ${worker_list}; do ${CTL} start $${worker}; done
	for i in {12900..12909}; do ${CTL} start 'swan:swan-web-'$${i}; done

stop:
	for worker in ${worker_list}; do ${CTL} stop $${worker}; done
	for i in {12900..12909}; do ${CTL} stop 'swan:swan-web-'$${i}; done

restart:
	for worker in ${worker_list}; do ${CTL} restart $${worker}; done
	for i in {12900..12909}; do ${CTL} restart 'swan:swan-web-'$${i}; done

status:
	${CTL} status "swan:"

env:
	${GIT} pull origin master
	${GIT} submodule update --init --recursive

update:
	make env
	make restart

clean:
	find . -name '*.pyc' -delete
	find . -name '*.py~' -delete
	find . -name '*.pyo' -delete

