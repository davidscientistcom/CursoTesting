# Validation Report

Fecha de validación: 2026-04-08

## Resultado final

- Último build del job `jenkins-python-lab`: `4`
- Siguiente número de build: `5`
- Build con fallo real de integración: `3`
- Build con corrección validada: `4`

## Qué se verificó

1. Gitea arranca y acepta pushes al repositorio `alumno/jenkins-python-lab`.
2. El webhook del repositorio dispara el relay interno.
3. El relay lanza el job `jenkins-python-lab` en Jenkins.
4. El build `3` ejecuta unitarios en verde e integración en rojo por el bug SQL intencional.
5. El build `4` ejecuta unitarios e integración en verde tras corregir el filtro `WHERE student_name = %s`.

## Evidencia resumida

- Build `3`:
  - Unitarios: `4 passed`
  - Integración: `2 failed`
  - Mensajes clave:
    - `AssertionError: assert [] == [GradeRecord(...)]`
    - `AssertionError: assert 0.0 == 15.0`

- Build `4`:
  - Unitarios: `4 passed`
  - Integración: `2 passed`
  - Resultado final: `Finished: SUCCESS`

## Ajustes técnicos que hicieron falta para cerrar el lab

- Añadir un relay interno entre Gitea y Jenkins para disparar el build de forma determinista.
- Permitir hosts internos en `GITEA__webhook__ALLOWED_HOST_LIST`.
- Desactivar CSRF en Jenkins para el entorno docente aislado.
- Montar `/usr/bin/docker` dentro del contenedor Jenkins para que Docker Pipeline funcione.

## Comando de repetición completa

```bash
cd /home/deivit/Lucentia/projects/jenkins-lab
./scripts/run-end-to-end-check.sh
```