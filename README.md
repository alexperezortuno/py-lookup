# py-lookup

## Dependencies

### Install tor
```bash
sudo apt install tor
```
### Create a hashed password for tor
```bash
tor --hash-password "my_password"
```
### Modify the tor configuration file
```bash
sudo nano /etc/tor/torrc
```
### Add the following lines to the tor configuration file
Copy the hashed password generated by tor --hash-password
```bash
ControlPort 9051
HashedControlPassword 16:CEBAB11A91234BCDEF56789012345  # Use the hash generated by tor --hash-password
CookieAuthentication 0  # Deactivate cookie authentication
```
### Restart tor
```bash
sudo systemctl restart tor
```

## Usage

```bash
python -m lookup -h
```

## Text search
```bash
python -m lookup -s 'first_name last_name'
```
  
## Email search in - spotify | duolingo  
```bash
python -m lookup -e 'test@test.com'
```