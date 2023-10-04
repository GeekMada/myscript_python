import os
import subprocess

def list_vhosts():
    try:
        active_vhosts = subprocess.check_output(["a2query", "-s"]).decode().split("\n")
        inactive_vhosts = subprocess.check_output(["a2query", "-sd"]).decode().split("\n")
        print("Vhosts actifs:")
        for vhost in active_vhosts:
            print(vhost)
        print("\nVhosts inactifs:")
        for vhost in inactive_vhosts:
            print(vhost)
    except Exception as e:
        print(f"Erreur: {e}")

def add_vhost(vhost_name):
    try:
        vhost_path = f"/etc/apache2/sites-available/{vhost_name}.conf"
        with open(vhost_path, "w") as f:
            f.write(f"""<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName {vhost_name}
    DocumentRoot /var/www/{vhost_name}
    ErrorLog ${{{vhost_name}}}/error.log
    CustomLog ${{{vhost_name}}}/access.log combined
</VirtualHost>""")
        os.makedirs(f"/var/www/{vhost_name}")
        subprocess.run(["a2ensite", vhost_name])
        subprocess.run(["systemctl", "reload", "apache2"])
    except Exception as e:
        print(f"Erreur: {e}")

def delete_vhost(vhost_name):
    try:
        subprocess.run(["a2dissite", vhost_name])
        subprocess.run(["rm", f"/etc/apache2/sites-available/{vhost_name}.conf"])
        subprocess.run(["systemctl", "reload", "apache2"])
    except Exception as e:
        print(f"Erreur: {e}")

def delete_vhost_and_dir(vhost_name):
    delete_vhost(vhost_name)
    try:
        subprocess.run(["rm", "-r", f"/var/www/{vhost_name}"])
    except Exception as e:
        print(f"Erreur: {e}")

def disable_vhost(vhost_name):
    try:
        subprocess.run(["a2dissite", vhost_name])
        subprocess.run(["systemctl", "reload", "apache2"])
    except Exception as e:
        print(f"Erreur: {e}")

def enable_certbot(vhost_name):
    try:
        subprocess.run(["certbot", "--apache", "-d", vhost_name])
    except Exception as e:
        print(f"Erreur: {e}")

def main():
    while True:
        print("""
1. Afficher la liste des vhosts
2. Ajouter un vhost
3. Supprimer un vhost
4. Supprimer un vhost et son répertoire
5. Désactiver un vhost
6. Activer Certbot pour un vhost
7. Quitter
""")
        choice = input("Choisissez une option: ")
        if choice == "1":
            list_vhosts()
        elif choice == "2":
            vhost_name = input("Entrez le nom du vhost: ")
            add_vhost(vhost_name)
        elif choice == "3":
            vhost_name = input("Entrez le nom du vhost à supprimer: ")
            delete_vhost(vhost_name)
        elif choice == "4":
            vhost_name = input("Entrez le nom du vhost et du répertoire à supprimer: ")
            delete_vhost_and_dir(vhost_name)
        elif choice == "5":
            vhost_name = input("Entrez le nom du vhost à désactiver: ")
            disable_vhost(vhost_name)
        elif choice == "6":
            vhost_name = input("Entrez le nom du vhost pour lequel activer Certbot: ")
            enable_certbot(vhost_name)
        elif choice == "7":
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Ce script doit être exécuté avec des privilèges d'administrateur (sudo).")
        exit(1)
    main()
