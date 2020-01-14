$(document).ready(function() {
  $("#skin_tones li:nth-child(1)").addClass("selected");
  $("#hair_tones li:nth-child(1)").addClass("selected");
  document.td_ids = [];
  document.skin_tone = $("#skin_tones li.selected").data("tone");
  document.hair_tone = $("#hair_tones li.selected").data("tone");

  var get_avatar_url = function() {
    var url = "/avatar/view3d?";

    for (var i = 0; i < document.td_ids.length; i += 1) {
      url += "&ids[]=" + document.td_ids[i];
    }
    url += "&skinTone=" + document.skin_tone;
    url += "&hairTone=" + document.hair_tone;
    return url;
  };

  $(".tdselection").click(function(e) {
    e.preventDefault();
    $(this)
      .parents(".category")
      .find(".selected")
      .removeClass("selected");
    $(this).addClass("selected");
    document.td_ids = [];
    $(".tdselection.selected").each(function() {
      document.td_ids.push($(this).data("id"));
    });
    $("#tdavatartarget").attr("src", get_avatar_url());
  });

  $("#skin_tones li").click(function(e) {
    e.preventDefault();
    $(this)
      .parents("#skin_tones")
      .find(".selected")
      .removeClass("selected");
    $(this).addClass("selected");
    document.skin_tone = $(this).data("tone");
    update_all_options();
  });

  var update_all_options = function() {
    $("#tdavatartarget").attr("src", get_avatar_url());
    $(".tdselection").each(function() {
      var new_url =
        $(this).data("src") +
        "&skinTone=" +
        document.skin_tone +
        "&hairTone=" +
        document.hair_tone;

      $(this).data("altsrc", new_url);
      $(this).attr("src", "");
    });
    $(".tdselection:visible").each(function() {
      $(this).attr("src", $(this).data("altsrc"));
    });
  };

  $("#hair_tones li").click(function(e) {
    e.preventDefault();
    $(this)
      .parents("#hair_tones")
      .find(".selected")
      .removeClass("selected");
    $(this).addClass("selected");
    document.hair_tone = $(this).data("tone");
    update_all_options();
  });

  $("#random-3d-avatar-button").click(function(e) {
    e.preventDefault();
    $(".select_avatar_type").each(function() {
      var catclass = $(this).data("target");

      $(".category." + catclass + " .tdselection")
        .random()
        .click();
    });
    $("#skin_tones li")
      .random()
      .click();
    $("#hair_tones li")
      .random()
      .click();
  });

  $(".select_avatar_type").click(function(e) {
    e.preventDefault();
    var target = $(this).data("target");

    $(".select_avatar_type").removeClass("active");
    $(this).addClass("active");
    $("#avatars-builder-3d .category").addClass("hidden");
    $("#avatars-builder-3d ." + target).removeClass("hidden");
    $("#avatars-builder-3d ." + target + " img").each(function() {
      if (!$(this).attr("src")) {
        var src = $(this).data("altsrc");

        $(this).attr("src", src);
      }
    });
  });

  async function save3DAvatarTo3Box() {
    var repoPath = `ipfs-${Math.random()}`;
    var ipfs = await Ipfs.create({ repo: repoPath });

    var directoryName = "directory";

    $(document).ajaxStart(function() {
      loading_button($("#save-3d--avatar"));
    });

    $(document).ajaxStop(function() {
      unloading_button($("#save-3d-avatar"));
    });

    var url = get_avatar_url();

    try {
      fetch(url, {
        method: "POST",
        body: JSON.stringify({ save: true }),
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        }
      })
        .then(response => response.text())
        .then(response => {
          window.ethereum.enable().then(async function(accounts) {
            Box.openBox(accounts[0], window.ethereum, {}).then(async function(
              box
            ) {
              const file = {
                path: `${directoryName}/avatar.svg`,
                content: new Blob([response], {
                  type: "image/svg+xml"
                })
              };
              ipfs.add(file, function(err, hash) {
                if (err) {
                  let text = gettext(
                    "Error occurred while saving. Please try again."
                  );
                  _alert({ message: text }, "error");
                } else {
                  box.public
                    .set("ethdenver.avatar", `/ipfs/${hash[1].hash}/avatar.svg`)
                    .then(success => {
                      const imgObj = [
                        {
                          "@type": "ImageObject",
                          contentUrl: {
                            "/": `${hash[1].hash}/avatar.svg`
                          }
                        }
                      ];
                      box.public.set("image", imgObj).then(result => {
                        _alert(
                          {
                            message: gettext(
                              "Your avatar has been saved using your eth address on 3box!"
                            )
                          },
                          "success"
                        );
                        box.close();
                      });
                    });
                }
              });
            });
          });
        });
    } catch (error) {
      let text = gettext("Error occurred while saving. Please try again.");
      _alert({ message: text }, "error");
    }
  }

  
  $("#save-3d-avatar").click(function(event) {
    event.preventDefault();
    save3DAvatarTo3Box();
  });

  jQuery.fn.random = function() {
    var randomIndex = Math.floor(Math.random() * this.length);

    return jQuery(this[randomIndex]);
  };
});
