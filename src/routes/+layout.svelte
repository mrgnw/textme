<script>
  export let data;
</script>

<slot></slot>

<layout>
	<pre><code>{JSON.stringify(data, null, 2)}</code></pre>
</layout>
