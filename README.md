# Setup
Create VM:
1. Start menu: Turn windows features on or off  
![](images/1-features.png)
2. Enable Hyper-V  
![](images/2-hyperv.png)
3. Restart computer
4. Open Hyper-V Manager  
![](images/4-manager.png)
5. Quick create on right menu  
![](images/5-create.png)
6. Choose Ubuntu 18.04 LTS image and click Crate Virtual Machine
7. Wait for image to download :)
8. Edit settings and configure with 8GB of RAM  
![](images/8-ram.png)
9. Start VM and configure Ubuntu settings - WRITE DOWN USER+PASS!

Install deps:
```bash
sudo apt update --fix-missing
sudo apt update
sudo apt install -y ca-certificates git wget curl vim gcc make zlib1g-dev libssl-dev libffi-dev
curl https://pyenv.run | bash
```

Add to `~/.bashrc`:
```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

Reload shell settings:
```bash
source ~/.bashrc
```

Install Python:
```bash
pyenv install -s 3.9.0
pyenv global 3.9.0
```

Finally, clone our repo:
```bash
git clone https://github.com/dolevelbaz/odyssey2021.git
```

Install packages:
TBD

# Exercise Stages
1. Implement rate limit for packets for a single core (fill in logic)
2. Test performance with sample attacker and benchmark (provided in exercise).
3. Run on multiple cores. Test performance again and compare
4. Optimize and continue benchmarking.
