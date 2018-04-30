<template>
  <transition-group name="pop" :tag="tag">
    <slot />
  </transition-group>
</template>

<script>
export default {
  name: 'PopGroup',
  props: {
    tag: {
      type: String,
      default: 'div',
    },
  },
}
</script>


<style lang="scss">
.pop-enter, 
.pop-leave-to {
  transform: scale(0) !important;
  opacity: 0 !important;
}
</style>
