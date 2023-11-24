ARCH="x86-64"
#ARCH="aarch64"

sudo whoami
apt-get -y install bison libtool python3.10 xz-utils curl autoconf automake unzip git pkg-config python3.10-dev ftp python3-pip vim texinfo ninja-build cmake libssl-dev wget yasm
python3.10 -m pip install bitarray pyelftools==0.28 psutil protobuf==3.20.3 leb128 capstone==5.0.0 keystone-engine
cp -r /ccr/src/randomizer /ccr/

# =======================================================
# Step 1. Install Protobuf
cd /ccr
wget https://github.com/protocolbuffers/protobuf/archive/refs/tags/v3.21.10.tar.gz
tar -xvf v3.21.10.tar.gz
rm -rf v3.21.10.tar.gz
mv protobuf-3.21.10 protobuf
cd protobuf
#proxychains git submodule update --init --recursive
./autogen.sh
./configure
make -j$(nproc)
sudo make install
sudo ldconfig

cd /ccr
wget https://github.com/protobuf-c/protobuf-c/archive/refs/tags/v1.4.1.tar.gz
tar -xvf v1.4.1.tar.gz
rm -rf v1.4.1.tar.gz
mv protobuf-c-1.4.1 protobuf-c
cd protobuf-c
./autogen.sh
./configure
make -j$(nproc)
sudo make install
sudo ldconfig


# =======================================================
# Step 2. Setup binutils-2.36.1
cd /ccr
wget https://ftp.gnu.org/gnu/binutils/binutils-2.36.1.tar.xz
tar -xvf binutils-2.36.1.tar.xz
rm -rf binutils-2.36.1.tar.xz
mv binutils-2.36.1 binutils-2.36.1-nocompiler
cd binutils-2.36.1-nocompiler
rm -rf gas
rm -rf gold
cp -r /ccr/src/gas .
cp -r /ccr/src/gold .

# sudo proto.sh binutils36-nocompiler
cp -r /ccr/src/protobuf_def /ccr/
cd /ccr/protobuf_def
protobuf=/ccr/protobuf_def
protoc --proto_path="$protobuf" --cpp_out=. "$protobuf/shuffleInfo.proto"
protoc --proto_path="$protobuf" --c_out=. "$protobuf/shuffleInfo.proto"
protoc --proto_path="$protobuf" --python_out=. "$protobuf/shuffleInfo.proto"
g++ -fPIC -g -shared "$protobuf/shuffleInfo.pb.cc" -o "$protobuf/shuffleInfo.so" `pkg-config --cflags --libs protobuf`

USER=`whoami`
chmod 755 "$protobuf/shuffleInfo.so"
chown $USER:$USER "$protobuf/shuffleInfo.so" "$protobuf/shuffleInfo.pb.cc" "$protobuf/shuffleInfo_pb2.py"

sudo cp "$protobuf/shuffleInfo.so" "/usr/lib/shuffleInfo.so"
sudo cp "$protobuf/shuffleInfo.so" "/usr/lib/libshuffleInfo.so"
sudo cp "$protobuf/shuffleInfo.so" "/usr/local/lib/shuffleInfo.so"
sudo cp "$protobuf/shuffleInfo.so" "/usr/local/lib/libshuffleInfo.so"
sudo cp "$protobuf/shuffleInfo_pb2.py" "/ccr/randomizer/shuffleInfo_pb2.py"
sudo cp "$protobuf/shuffleInfo.proto" "/ccr/randomizer/shuffleInfo.proto"
sudo cp "$protobuf/shuffleInfo.pb.h" "/usr/local/include/shuffleInfo.pb.h"



# =======================================================
# Step 3. Compile binutils
cd /ccr/binutils-2.36.1-nocompiler
if [ $ARCH = "x86-64" ]
then
  mkdir build-x64-release
  cd build-x64-release
  ../configure --enable-gold --enable-plugins LDFLAGS='-Wl,--no-as-needed -L/usr/local/lib -lprotobuf-c -lprotobuf -lshuffleInfo'
else
  mkdir build-arm64-release
  cd build-arm64-release
  ../configure --enable-gold --enable-plugins LDFLAGS='-L/usr/local/lib -lshuffleInfo -lprotobuf-c -lprotobuf' LIBS='-lshuffleInfo -lprotobuf-c -lprotobuf' --target=aarch64-linux-gnu --disable-multilib --with-arch=armv8 --disable-libsanitizer
fi
sudo make -j$(nproc)


# =======================================================
# Step 4. 选装myrust 1.67.0
# cd /ccr/
# git clone https://github.com/rust-lang/rust.git myrust67
# cd myrust67
# git checkout 1.67.0
# git submodule update --init --recursive
# cp -r /ccr/src/myrust67-patch/* .
# ./x.py build --stage 1 -j$(nproc)
# if [ $ARCH = "x86-64" ]
# then
#   rm /ccr/myrust67/build/x86_64-unknown-linux-gnu/stage1-std
#   sudo ld.sh np-x64
# else
#   rm /ccr/myrust67/build/aarch64-unknown-linux-gnu/stage1-std
#   sudo ld.sh np-arm64
# fi
# ./x.py build --stage 1 -j$(nproc)
# sudo ld.sh gcc10

# cd /ccr/
# wget https://sh.rustup.rs/rustup-init.sh
# chmod 777 rustup-init.sh
# ./rustup-init.sh
# source "$HOME/.cargo/env"
# if [ $ARCH = "x86-64" ]
# then
#   rustup toolchain link myrust67 /ccr/myrust67/build/x86_64-unknown-linux-gnu/stage1
# else
#   rustup toolchain link myrust67 /ccr/myrust67/build/aarch64-unknown-linux-gnu/stage1
# fi
# rustup default myrust67

sudo rm /usr/bin/ld
sudo rm /usr/bin/as
if [ $ARCH = "x86-64" ]
then
  ln -s /ccr/binutils-2.36.1-nocompiler/build-x64-release/gold/ld-new /usr/bin/ld
  ln -s /ccr/binutils-2.36.1-nocompiler/build-x64-release/gas/as-new /usr/bin/as
else
  ln -s /ccr/binutils-2.36.1-nocompiler/build-arm64-release/gold/ld-new /usr/bin/ld
  ln -s /ccr/binutils-2.36.1-nocompiler/build-arm64-release/gas/as-new /usr/bin/as
fi
