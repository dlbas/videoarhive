Vagrant.configure("2") do |config|
    config.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 2
    end

    config.vm.box = "debian/contrib-buster64"

    config.vm.network "forwarded_port", guest: 8080, host: 8080

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "./ansible/playbook.yml"
    end
  
  end
  