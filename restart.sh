# /usr/bin/bash
sudo systemctl stop gptquizweb.service
sudo systemctl start gptquizweb.service

sudo systemctl stop gptquiz.service
sudo systemctl start gptquiz.service
