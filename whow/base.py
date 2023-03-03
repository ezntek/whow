#    Copyright 2023 ezntek (ezntek@xflymusic.com) and DaringCuteSeal (daringcuteseal@gmail.com)
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
    
#      http://www.apache.org/licenses/LICENSE-2.0
    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import shutil
import util
import config

import colors.colors as colors
import data_structures.category as category

import tomli_w as toml_writer

def init(destroy: bool = False, verbose: bool = True) -> None:
    """
    Create the necessary paths for the To-Dos and Events.
    """
    cfg = config.Config() # no existing config exists yet
    
    util.log("Reconfiguring Whow...") if verbose else None

    if destroy:
        util.warn(f"Overwriting {cfg.config_tree_dir} and {cfg.data_tree_dir}...")
        try:
            cfg.nuke_cfg()
            shutil.rmtree(cfg.config_tree_dir)
            shutil.rmtree(cfg.data_tree_dir)
        except FileNotFoundError:
            pass

    # create dirs
    dirs = [
        cfg.data_tree_dir,
        os.path.join(os.environ['HOME'], "./.config/whow")
    ]

    tree_dirs = [
            "todos",
            "categories",
            "events",
    ]

    for dir in dirs:
        if not os.path.isdir(dir):
            util.log(f"Created directory {dir}.") if verbose else None
            os.mkdir(dir)

    for dir in tree_dirs:
        if not os.path.isdir(os.path.join(cfg.data_tree_dir, dir)):
            util.log(f"Created directory {dir}.") if verbose else None
            os.mkdir(os.path.join(cfg.data_tree_dir, dir))
    
    indextoml_tmp = toml_writer.dumps(
        {
            "indexes": [] # type: ignore
        }
    )

    # write the index.toml's
    todos_indextoml = open(os.path.join(cfg.data_tree_dir, 'todos/index.toml'), "w+")
    events_indextoml = open(os.path.join(cfg.data_tree_dir, 'events/index.toml'), "w+") 
    todos_indextoml.write(indextoml_tmp)
    events_indextoml.write(indextoml_tmp)

    todos_indextoml.close()
    events_indextoml.close()

    # create the default config.toml
    util.log("Writing configuration file...") if verbose else None
    cfg.write_cfg(quiet=True)
    
    # create a new important category
    util.log("Registering important category...") if verbose else None
    category.register_category(category.Category("important", colors.RED), cfg, force=True)