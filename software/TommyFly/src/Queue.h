#ifndef QUEUE
#define QUEUE

template <typename T, int N>
class RingQueue {

public:
    RingQueue() : ringbuffer_(), from_index(0), to_index(0) {
        for(int i = 0; i < N; i++) {
            ringbuffer_[i] = T();
        }
    }

    ~RingQueue() {
    }

    void push(T elem) {
        if(to_index == N - 1) {
            to_index = 0;
        } else {
            to_index++;
        }
        ringbuffer_[to_index] = elem;
    }

    T pop() {
        int old_index  = from_index;
        if(from_index == N - 1) {
            from_index = 0;
        } else {
            from_index++;
        }
        return ringbuffer_[old_index];        
    }

    T sum() {
        T sum = 0;
        if(from_index <= to_index) {
            for(int i = from_index; i <= to_index; i++) {
                sum = sum + ringbuffer_[i];
            }
        }
        else {
            for(int i = from_index; i < N; i++) {
                sum = sum + ringbuffer_[i];
            }

            for(int i = 0; i <= to_index; i++) {
                sum = sum + ringbuffer_[i];
            }
        }
        return sum;
    }

    int length() {
        if(from_index <= to_index) {
            return to_index - from_index + 1;
        }
        else {
            return (N - from_index) + (to_index + 1);
        }
    }

private:

    T ringbuffer_[N];

    int from_index;

    int to_index;

};

#endif
