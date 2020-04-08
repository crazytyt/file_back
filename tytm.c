
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <ctype.h>
#include <termios.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <stdbool.h>
#include <stdint.h>

#define FATAL do { fprintf(stderr, "Error at line %d, file %s (%d) [%s]\n", \
		__LINE__, __FILE__, errno, strerror(errno)); exit(1); } while(0)

#define MAP_SIZE 4096UL
#define MAP_MASK (MAP_SIZE - 1)

#ifdef DEBUG
#define debug(fmt, args...) printf(fmt, ##args)
#else
#define debug()
#endif

#define DEBUG

static inline void *fixup_addr(void *addr, size_t size)
{
	unsigned long aligned_addr = (unsigned long)addr;
	aligned_addr &= ~(size - 1);
	addr = (void *)aligned_addr;

	return addr;
}

void usage(void)
{
	printf("\nUsage: { r/w } { address } {  value/len  } \n"
		"\tr/w : read or write\n"
		"\taddress : memory address to act upon\n"
		"\tvalue/len     : value to write or len to read\n\n");

}

int main(int argc, char **argv) {
	int fd, i, j = 4;
	void *map_base, *virt_addr; 
	unsigned int offset, len;
	off_t target_addr;
	int access_type = 'w';
	char fmt_str[128];
	size_t data_size;
	char rw = 'r';
	uint64_t l1, l2;
	uint32_t n1, n2;

	if(argc != 4) {
		usage();
		exit(1);
	}

	rw = argv[1][0];
	if (rw != 'r' && rw != 'w') {
		usage();
		exit(1);
	}

	target_addr = strtoul(argv[2], 0, 0);
	len = strtoul(argv[3], 0, 0);
	if (rw == 'r' && len > 1000) {
		printf(" len should be less than 1000\n");
		usage();
		exit(1);
	}

	offset = target_addr & MAP_MASK;
	if (target_addr > 0xFFFFFFFF)
		j = 8;

	if((fd = open("/dev/mem", O_RDWR | O_SYNC)) == -1) FATAL;
	fflush(stdout);

	/* Map one page */
	map_base = mmap(0, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, target_addr & ~MAP_MASK);
	if(map_base == (void *) -1) FATAL;
	//debug("Memory mapped at address %p.\n", map_base); 
	fflush(stdout);

	// 4 bytes or 8 bytes align
	virt_addr = map_base + (target_addr & MAP_MASK);
	if (j == 4) {
		virt_addr = (void *)((unsigned long )virt_addr & ~3L);
		target_addr &= ~0x3L;
	} else {
		virt_addr = (void *)((unsigned long )virt_addr & ~7L);
		target_addr &= ~0x7L;
	}

	if (rw == 'w') { // write the memory
		if (j == 4)
			*((unsigned int*) (virt_addr)) = len;
		else
			*((unsigned long*) (virt_addr)) = len;
	} else { // read the memory
		if (j == 4)
			for (i = 0; i < len; i += 4)
			{
				printf("0x%08lx: %08x %08x %08x %08x\n",
						target_addr + i * j,
						*((unsigned int*) (virt_addr + i * j)),
						*((unsigned int*) (virt_addr + (i + 1) * j)),
						*((unsigned int*) (virt_addr + (i + 2) * j)),
						*((unsigned int*) (virt_addr + (i + 3) * j)));

			}
		else
			// output 4 numbers each so len / 2
			for (i = 0; i < len / 2; i += 2)
			{
				l1 = *((unsigned long*) (virt_addr + i * j));
				l2 = *((unsigned long*) (virt_addr + (i + 1) * j));

				// break the 64bits number into 2 32bits number
				printf("0x%016lx: %08x %08x %08x %08x\n",
						target_addr + i * j,
						l1, (l1 >> 32) & 0xFFFFFFFF,
						l2, (l2 >> 32) & 0xFFFFFFFF);
			}
	}

end:
	fflush(stdout);

	if(munmap(map_base, MAP_SIZE) == -1) FATAL;
	close(fd);

	return 0;
}
