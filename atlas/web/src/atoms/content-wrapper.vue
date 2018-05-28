<template>
  <div class="content-wrapper">
    <slot />
  </div>
</template>

<style lang="scss">
@import "./../_vars.scss";

.content-wrapper {
  margin: 0 auto;
  max-width: $content-width;
  width: 100%;
}

</style>

