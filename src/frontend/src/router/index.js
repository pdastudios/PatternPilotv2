import { createRouter, createWebHistory } from 'vue-router';
import PatternCalc from '@/components/PatternCalc.vue';
import PatternTrack from '@/components/PatternTrack.vue';

const routes = [
  { 
    path: '/', 
    redirect: '/calculate',
    component: {
      template: '<router-view/>',
  },
  children: [
    { 
      path: '/calculate', 
      name: 'PatternCalculation',
      component: PatternCalc 
    },
    { 
      path: '/track',
      name: 'PatternTracker',
      component: PatternTrack 
    }
  ]
}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
