#/bin/bash
cd ~
curl -s -L http://dl.tigergraph.com/developer-edition/tigergraph-3.0.0-developer.tar.gz -o tigergraph-dev.tar.gz
tar xfz tigergraph-dev.tar.gz
rm -f tigergraph-dev.tar.gz
cd tigergraph-*
sudo ./install.sh
cd ..
