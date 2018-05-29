<template>
  <div class="content-wrapper">
    <slot />
  </div>
</template>

<style lang="scss">
@import "./../_vars.scss";

.content-wrapper {
  margin: 0 auto;
  padding: 0 baseline();
  max-width: $content-width;
  width: 100%;

  @include on(desktop) {
    padding: 0;
  }
}

</style>

