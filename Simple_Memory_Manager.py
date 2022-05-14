class NotEnoughSpace(Exception):
    def __init__(self):
        print("error there is not enough space for allocation!")


class FreeUnallocatedBlock(Exception):
    def __init__(self):
        print("error cant free an unallocated block of memory")


class IndexOutOfBound(Exception):
    def __init__(self):
        print("error the index refers to unallocated memory")


class MemoryManager:
    def __init__(self, memory):
        """
        @constructor Creates a new memory manager for the provided array.
        @param {memory} An array to use as the backing memory.
        """
        self.memory = memory
        # contains pairs of [start, end] indexes of each allocation
        self.allocs = []

    def allocate(self, size):
        """
        Allocates a block of memory of requested size.
        @param {number} size - The size of the block to allocate.
        @returns {number} A pointer which is the index of the first location in the allocated block.
        @raises If it is not possible to allocate a block of the requested size.
        """
        if len(self.allocs) == 0 and size <= len(self.memory):
            self.allocs.append([0, size-1])
            return 0

        # checking weather we should insert as the first allocation
        if self.allocs[0][0] >= size:
            self.allocs.insert(0, [0, size-1])
            return 0

        # checking weather we should insert in the middle of the array
        i = 0
        while i < len(self.allocs) - 1:
            prev_end = self.allocs[i][1]
            if self.allocs[i+1][0] - prev_end - 1 >= size:
                self.allocs.insert(i+1, [prev_end+1, prev_end+size])
                return prev_end + 1
            i += 1

        # checking weather we should insert at the end of the array
        if i == len(self.allocs) - 1:
            prev_end = self.allocs[i][1]
            if len(self.memory) - prev_end - 1 >= size:
                self.allocs.append([prev_end + 1, prev_end + size])
                return prev_end + 1

        raise NotEnoughSpace

    def release(self, pointer):
        """
        Releases a previously allocated block of memory.
        @param {number} pointer - The pointer to the block to release.
        @raises If the pointer does not point to an allocated block.
        """
        i = 0
        while i < len(self.allocs):
            if self.allocs[i][0] == pointer:
                del self.allocs[i]
                return
            i += 1

        raise FreeUnallocatedBlock

    def read(self, pointer):
        """
        Reads the value at the location identified by pointer
        @param {number} pointer - The location to read.
        @returns {number} The value at that location.
        @raises If pointer is in unallocated memory.
        """
        i = 0
        while i < len(self.allocs):
            if self.allocs[i][0] <= pointer <= self.allocs[i][1]:
                return self.memory[pointer]
            i += 1

        raise IndexOutOfBound

    def write(self, pointer, value):
        """
        Writes a value to the location identified by pointer
        @param {number} pointer - The location to write to.
        @param {number} value - The value to write.
        @raises If pointer is in unallocated memory.
        """
        i = 0
        while i < len(self.allocs):
            if self.allocs[i][0] <= pointer <= self.allocs[i][1]:
                self.memory[pointer] = value
                return
            i += 1

        raise IndexOutOfBound
