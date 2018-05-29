<template>
  <div class="tab-container">
    <slot />
  </div>
</template>

<style lang="scss">
@import "./../_vars.scss";

.tab-container {
  @include row();
}
</style>

