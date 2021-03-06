<%namespace file='aarau:templates/macro/_flash_message.mako' import="render_notice"/>
<%namespace file='aarau:templates/macro/_title.mako' import="render_title"/>

<%inherit file='aarau:templates/console/_layout.mako'/>

<%block name='title'>${render_title('{:s} - {:s} - {:s}'.format(_('title.settings.scripts'), site.instance.name, project.name))}</%block>

<%block name='breadcrumb'>
<div class="breadcrumb">
  <span class="divider">/</span>
  <%include file='aarau:templates/console/site/application/_breadcrumb_parent_items.mako'/>
  <span class="item active">${_('title.settings.scripts')}</span>
</div>
</%block>

<%block name='sidebar'>
  <%include file='aarau:templates/console/site/application/_sidebar_settings.mako'/>
</%block>

<%block name='footer'>
</%block>

<div id="application" class="content">
  <div class="grid">
    <div class="row">
      <div class="column-16">
        ${render_notice()}
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <h4>${instance.name}</h4>
        <label class="application label">${site.domain}</label>
      </div>
    </div>

    <div class="row">
      <div class="column-16">
        <div class="attached header">
          <h5>Readability Measure Scripts</h5>
        </div>

        <div class="attached box">
          <div class="row">
            <div class="column-16">
              % if credentials_state:
                <label class="positive label">Ready</label>
              % else:
                <label class="label">In Sync...</label>
              % endif

              <p class="description">Set <code>PROJECT_ID</code> and configure <label class="primary label">WRITE_KEY</label> as `apiKey` with yours. You can just paste this snippet at the bottom of body of your article. The script will work based on user&apos;s scroll. At least, you need to include this for readability analysis of your texts.</p>
              <p class="description">The source code is available from also <a href="https://gitlab.com/scrolliris/scrolliris-readability-tracker" target="_blank">our repository</a>. (Code Name: Stäfa)</p>

              <h6>Position</h6>
              <pre class="inverted">(function(d, w) {
  var config = {
      projectId: '${project.access_key_id}'
    , apiKey: '${site.write_key}'
    }
  , settings = {
      endpointURL: 'https://api.scrolliris.com/v1.0/projects/'+config.projectId+'/events/read'
    }
  , options = {}
  ;
  var a,c=config,f=false,k=d.createElement('script'),s=d.getElementsByTagName('script')[0];k.src='https://lib.scrolliris.com/script/v1.0/projects/'+c.projectId+'/measure.js?api_key='+c.apiKey;k.async=true;k.onload=k.onreadystatechange=function(){a=this.readyState;if(f||a&&a!='complete'&&a!='loaded')return;f=true;try{var r=w.ScrollirisReadabilityTracker,t=(new r.Client(c,settings));t.ready(['body'],function(){t.record(options);});}catch(_){}};s.parentNode.insertBefore(k,s);
})(document, window);</pre>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</div>
