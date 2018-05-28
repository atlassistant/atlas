<template>
  <div class="administration">
    <topbar />
    <router-view />
  </div>
</template>

<script>
import {
  Topbar,
} from './../organisms';

export default {
  name: 'Administration',
  components: {
    Topbar,
  },
}
</script>


<style lang="scss">
@import "./../_vars.scss";

.administration {
  @include cell();
  background-color: color(background, 1);
}

</style>
