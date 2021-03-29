# videoarhive

A videoarchive application featuring encoding to different formats & storage.

## How to run

You need to have `vagrant` installed and probably `virtualbox`, since it's the easiest way to run boxes on different platforms.

To create the machine simply run:
```vagrant up```

Then, open your browser at http://localhost:8080.

Vagrant runs `ansible` playbook, located in `ansible/`. Feel free to use variables in `ansible/playbook.yml` to make changes.

## Development
You can use docker-compose which replicates vagrant vm for local development.
