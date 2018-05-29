<template>
  <div class="administration">
    <topbar />
    <breadcrumb />
    <router-view />
  </div>
</template>

<script>
import {
  Breadcrumb,
} from './../molecules';

import {
  Topbar,
} from './../organisms';

export default {
  name: 'Administration',
  components: {
    Topbar,
    Breadcrumb,
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
