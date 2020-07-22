
export CROSS_COMPILE=/opt/fsl-qoriq/3.0/sysroots/x86_64-fslsdk-linux/usr/bin/aarch64-fsl-linux/aarch64-fsl-linux-
export ARCH=arm64

KERNEL_DIR=/mnt/dash-lts

obj-m = runtime_pm.o

all:
	make -C $(KERNEL_DIR) M=$(PWD) modules

clean:
	make -C $(KERNEL_DIR) M=$(PWD) clean
