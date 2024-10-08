import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    stages: [
        { duration: '30s', target: 10 }, 
        { duration: '1m', target: 10 },  
        { duration: '30s', target: 0 },  
    ],
};

export default function () {
    let res = http.get('http://localhost:5000/pipeline'); 
    check(res, {
        'status was 200': (r) => r.status === 200,
        'transaction time OK': (r) => r.timings.duration < 200,
    });
    sleep(1);
}
