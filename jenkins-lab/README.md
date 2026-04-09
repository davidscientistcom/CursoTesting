# Jenkins Lab

Laboratorio reproducible para enseñar un flujo completo de CI con Jenkins, Gitea, pytest y MariaDB.

## Qué incluye

- `docker-compose.yml`: stack local con Jenkins y Gitea.
- `webhook-relay/`: puente interno entre el webhook de Gitea y el endpoint de build de Jenkins.
- `jenkins/`: imagen reproducible de Jenkins con plugins e init scripts.
- `repo-template/`: aplicación Python y `Jenkinsfile` que se publican en Gitea para la demo.
- `scripts/`: automatización de arranque, bootstrap y verificación end-to-end.
- `docs/`: guía paso a paso en formato HTML.

## Arranque rápido

```bash
cd /home/deivit/Lucentia/projects/jenkins-lab
./scripts/run-end-to-end-check.sh
```

## Credenciales del laboratorio

- Jenkins admin: `admin` / `jenkinsadmin2026`
- Jenkins lectura: `alumno` / `alumno2026`
- Gitea alumno: `alumno` / `alumno2026`

## URLs

- Jenkins: `http://localhost:9090`
- Gitea: `http://localhost:3000`

## Flujo demostrado

1. Se levanta Jenkins y Gitea.
2. Se crea el repositorio `alumno/jenkins-python-lab` en Gitea.
3. Jenkins queda preparado con un job `Pipeline script from SCM`.
4. El webhook de Gitea llama al relay interno y este dispara el build de Jenkins.
5. Un primer push introduce un bug en el adaptador MariaDB: los unit tests pasan y los integration tests fallan.
6. Un segundo push corrige el bug y el pipeline pasa en verde.