<template>
  <CFooter :fixed="false">
    <div>
      <span class="ml-auto">Hutech Management</span>
      <span class="mr-1">&copy; {{ new Date().getFullYear() }} by</span>
      <a href="https://mypeaga.xyz" target="_blank">Peaga inc.</a>
    </div>
  </CFooter>
</template>

<script>
export default {
  name: "TheFooter"
};
</script>
