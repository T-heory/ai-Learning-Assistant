import { ref, computed, onMounted, onUnmounted } from 'vue'

const BREAKPOINTS = { MOBILE: 768, TABLET: 1024 }

export function useDevice() {
  const windowWidth = ref(window.innerWidth)

  const handleResize = () => { windowWidth.value = window.innerWidth }

  onMounted(() => window.addEventListener('resize', handleResize))
  onUnmounted(() => window.removeEventListener('resize', handleResize))

  const isMobile = computed(() => windowWidth.value < BREAKPOINTS.MOBILE)
  const isTablet = computed(() =>
    windowWidth.value >= BREAKPOINTS.MOBILE && windowWidth.value < BREAKPOINTS.TABLET)
  const isDesktop = computed(() => windowWidth.value >= BREAKPOINTS.TABLET)
  const deviceType = computed(() =>
    isMobile.value ? 'mobile' : isTablet.value ? 'tablet' : 'desktop')

  return { isMobile, isTablet, isDesktop, deviceType, windowWidth }
}
